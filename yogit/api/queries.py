"""
GraphQL queries used by yogit
"""
import textwrap

import click
from tabulate import tabulate

import yogit.api.statements as S
from yogit.api.client import GraphQLClient, RESTClient
from yogit.api.statement import prepare, prepare_pagination
from yogit.utils.dateutils import dt_for_str, days_ago_str
from yogit.utils.spinner import spin


def shorten_str(full_string):
    """
    Shorten string to 50 chars max, including an ending ellipsis
    Words are not truncated
    """
    return textwrap.shorten(full_string, width=50, placeholder="...")


class Query:
    """ Represent a GitHub query """

    def __init__(self):
        self._response = []
        self.client = None

    def _handle_response(self, response):
        self._response.append(response)

    def execute(self):
        """ Execute the query """
        raise NotImplementedError()

    def tabulate(self):
        """ Return tabulated result """
        raise NotImplementedError()

    def print(self):
        """ Print result """
        click.echo(self._response)


class GraphQLQuery(Query):
    def __init__(self, statement, variables=[], extra_data={}, pagination_offset=None):
        super().__init__()
        self.client = GraphQLClient()
        self.statement = statement
        self.variables = variables
        self.extra_data = extra_data
        self.pagination_offset = pagination_offset

    def get_pagination_info(self):
        raise NotImplementedError()

    def get_count(self):
        raise NotImplementedError()

    @spin
    def execute(self, spinner):
        prepared_statement = prepare(self.statement, self.variables, self.extra_data)
        if self.pagination_offset is None:
            response = self.client.get(prepared_statement)
            super()._handle_response(response)
            self._handle_response(response)
            return

        cursor = None
        has_next = True
        while has_next:
            paginated_statement = prepare_pagination(prepared_statement, self.pagination_offset, cursor)
            response = self.client.get(paginated_statement)
            super()._handle_response(response)
            self._handle_response(response)
            count = self.get_count()
            if count > 0:
                spinner.text = "Loading... (yet {} entries found)".format(count)
            pagination_info = self.get_pagination_info(response)
            has_next = pagination_info["hasNextPage"]
            cursor = pagination_info["endCursor"]


class RESTQuery(Query):
    def __init__(self, endpoint):
        super().__init__()
        self.client = RESTClient()
        self.endpoint = endpoint

    @spin
    def execute(self, spinner):
        response = self.client.get(self.endpoint)
        super()._handle_response(response)
        self._handle_response(response)


class LoginQuery(GraphQLQuery):
    def __init__(self):
        super().__init__(S.LOGIN_STATEMENT)
        self.login = None

    def _handle_response(self, response):
        self.login = response["data"]["viewer"]["login"]

    def get_login(self):
        return self.login


class ReviewRequestedQuery(GraphQLQuery):
    def __init__(self, is_closed):
        self.is_closed = is_closed
        state = "closed" if self.is_closed else "open"
        super().__init__(
            S.REVIEW_REQUESTED_STATEMENT,
            variables=[S.LOGIN_VARIABLE],
            extra_data={"state": state},
            pagination_offset=100,
        )
        self.data = []

    def get_pagination_info(self, response):
        return response["data"]["search"]["pageInfo"]

    def get_count(self):
        return len(self.data)

    def _handle_response(self, response):
        for pr in response["data"]["search"]["edges"]:
            title = shorten_str(pr["node"]["title"])
            url = pr["node"]["url"]
            updated = dt_for_str(pr["node"]["updatedAt"]).date()
            updated_str = days_ago_str(updated)
            self.data.append([updated, updated_str, url, title])

        self.data = sorted(self.data, key=lambda x: (x[2], x[3]))
        self.data = sorted(self.data, key=lambda x: x[0], reverse=True)

    def print(self):
        if len(self.data) == 0:
            click.secho("All done! 🎉✨", bold=True)
        else:
            click.echo(tabulate([x[1:] for x in self.data], headers=["UPDATED", "PULL REQUEST", "TITLE"]))
            click.secho("Count: {}".format(len(self.data)), bold=True)


class ReviewListQuery(GraphQLQuery):
    def __init__(self):
        super().__init__(S.REVIEW_LIST_STATEMENT, pagination_offset=100)
        self.data = []

    def get_pagination_info(self, response):
        return response["data"]["viewer"]["contributionsCollection"]["pullRequestReviewContributions"]["pageInfo"]

    def get_count(self):
        return len(self.data)

    def _handle_response(self, response):
        for review in response["data"]["viewer"]["contributionsCollection"]["pullRequestReviewContributions"]["edges"]:
            pr_state = review["node"]["pullRequest"]["state"]
            if pr_state != "OPEN":
                continue

            url = review["node"]["pullRequest"]["url"]
            rv_state = review["node"]["pullRequestReview"]["state"]
            last_commit_pushed = dt_for_str(
                review["node"]["pullRequest"]["commits"]["edges"][0]["node"]["commit"]["pushedDate"]
            )

            rv_updated = review["node"]["pullRequestReview"]["updatedAt"]
            if rv_updated is None:
                rv_updated = review["node"]["pullRequestReview"]["createdAt"]
            rv_updated = dt_for_str(rv_updated)

            up_to_date = rv_updated > last_commit_pushed
            rv_updated_str = days_ago_str(rv_updated.date())

            rv_state_str = rv_state
            if not up_to_date:
                rv_state_str += " (new commits)"

            self.data.append([rv_updated.date(), rv_updated_str, url, rv_state_str])

        # Sort by url, then by reversed date:
        self.data = sorted(self.data, key=lambda x: x[2])
        self.data = sorted(self.data, key=lambda x: x[0], reverse=True)

    def print(self):
        if len(self.data) == 0:
            click.secho("Nothing... 😿", bold=True)
        else:
            click.echo(tabulate([x[1:] for x in self.data], headers=["UPDATED", "PULL REQUEST", "STATE"]))
            click.secho("Count: {}".format(len(self.data)), bold=True)


class OrganizationListQuery(GraphQLQuery):
    def __init__(self):
        super().__init__(S.ORGANIZATION_LIST_STATEMENT)
        self.data = []

    def _handle_response(self, response):
        orgas = response["data"]["viewer"]["organizations"]["edges"]
        for orga in orgas:
            login = orga["node"]["login"]
            url = orga["node"]["url"]
            self.data.append([login, url])

        self.data = sorted(self.data, key=lambda x: x[0].lower())

    def print(self):
        if len(self.data) == 0:
            click.secho("You do not belong to any organization 😿", bold=True)
        else:
            click.echo(tabulate(self.data, headers=["ORGANIZATION", "URL"]))
            click.secho("Count: {}".format(len(self.data)), bold=True)


class OrganizationMemberListQuery(GraphQLQuery):
    def __init__(self, organization):
        super().__init__(
            S.ORGANIZATION_MEMBER_LIST_STATEMENT, pagination_offset=100, extra_data={"organization": organization}
        )
        self.data = []
        self.organization = organization

    def get_pagination_info(self, response):
        return response["data"]["viewer"]["organization"]["membersWithRole"]["pageInfo"]

    def get_count(self):
        return len(self.data)

    def _handle_response(self, response):
        for member in response["data"]["viewer"]["organization"]["membersWithRole"]["edges"]:
            login = member["node"]["login"]
            email = member["node"]["email"]
            location = member["node"]["location"]
            role = member["role"]
            self.data.append([login, email, location, role])

        self.data = sorted(self.data, key=lambda x: x[0])

    def print(self):
        click.secho("{}'s members".format(self.organization), bold=True)
        click.echo(tabulate(self.data, headers=["NAME", "EMAIL", "LOCATION", "ROLE"]))
        click.secho("Count: {}".format(len(self.data)), bold=True)


class RateLimitQuery(GraphQLQuery):
    def __init__(self):
        super().__init__(S.RATE_LIMIT_STATEMENT)
        self.limit = None
        self.remaining = None
        self.reset_at = None

    def _handle_response(self, response):
        rate_limit = response["data"]["rateLimit"]
        self.limit = rate_limit["limit"]
        self.remaining = rate_limit["remaining"]
        self.reset_at = rate_limit["resetAt"]

    def print(self):
        click.secho("{}/{} until {}".format(self.remaining, self.limit, self.reset_at), bold=True)


class PullRequestListQuery(GraphQLQuery):
    def __init__(self):
        super().__init__(S.PULL_REQUEST_LIST_STATEMENT)
        self.data = []

    def _handle_response(self, response):
        for pr in response["data"]["viewer"]["pullRequests"]["edges"]:
            created = dt_for_str(pr["node"]["createdAt"]).date()
            url = pr["node"]["url"]
            title = shorten_str(pr["node"]["title"])
            mergeable = pr["node"]["mergeable"]
            created_str = days_ago_str(created)
            self.data.append([created, created_str, url, title, mergeable])
        # Sort by url, then by reversed date:
        self.data = sorted(self.data, key=lambda x: x[2])
        self.data = sorted(self.data, key=lambda x: x[0], reverse=True)

    def print(self):
        if len(self.data) == 0:
            click.secho("Nothing... 😿 Time to push hard 💪", bold=True)
        else:
            click.echo(tabulate([x[1:] for x in self.data], headers=["CREATED", "URL", "TITLE", "MERGEABLE"]))
            click.secho("Count: {}".format(len(self.data)), bold=True)


class OrgaPullRequestListQuery(GraphQLQuery):
    def __init__(self, organization):
        super().__init__(
            S.ORGA_PULL_REQUEST_LIST_STATEMENT, pagination_offset=10, extra_data={"organization": organization}
        )
        self.data = []

    def get_count(self):
        return len(self.data)

    def get_pagination_info(self, response):
        return response["data"]["search"]["pageInfo"]

    def _handle_response(self, response):
        for pr in response["data"]["search"]["edges"]:
            created = dt_for_str(pr["node"]["createdAt"]).date()
            url = pr["node"]["url"]
            title = shorten_str(pr["node"]["title"])
            created_str = days_ago_str(created)
            self.data.append([created, created_str, url, title])
        # Sort by url, then by reversed date:
        self.data = sorted(self.data, key=lambda x: x[2])
        self.data = sorted(self.data, key=lambda x: x[0], reverse=True)

    def print(self):
        if len(self.data) == 0:
            click.secho("Nothing... 😿 Time to push hard 💪", bold=True)
        else:
            click.echo(tabulate([x[1:] for x in self.data], headers=["CREATED", "URL", "TITLE"]))
            click.secho("Count: {}".format(len(self.data)), bold=True)


class ContributionListQuery:
    def __init__(self, dt_from, dt_to, organization=None):
        # TODO reengineer this class - create a generic one capable of executing
        #      queries sequentially
        self.pr_query = PullRequestContributionListQuery(dt_from, dt_to, organization)
        self.rv_query = PullRequestReviewContributionListQuery(dt_from, dt_to, organization)

    def execute(self):
        self.pr_query.execute()
        self.rv_query.execute()

    def print(self):
        data = []
        data.extend(self.pr_query.data)
        data.extend(self.rv_query.data)

        # Sort by url, then by reversed date:
        data = sorted(data, key=lambda x: (x[1], x[2], x[3]))
        data = sorted(data, key=lambda x: x[0], reverse=True)

        if len(data) == 0:
            click.secho("Nothing... 😿 Time to push hard 💪", bold=True)
        else:
            click.echo(tabulate(data, headers=["CREATED", "PULL REQUEST", "ROLE", "TITLE"]))
            click.secho("Count: {}".format(len(data)), bold=True)


class ContributionStatsQuery(GraphQLQuery):
    def __init__(self):
        super().__init__(S.CONTRIBUTION_STATS_STATEMENT)
        self.data = []

    def _handle_response(self, response):
        for k, v in response["data"]["viewer"]["contributionsCollection"].items():
            # `camelCase` to `Title case`
            key = "".join([" " + x.lower() if x.isupper() else x for x in k])
            key = key[0].upper() + key[1:]
            self.data.append([key, v])
        self.data = sorted(self.data, key=lambda x: x[0])

    def tabulate(self):
        return tabulate(self.data, headers=["STAT", "VALUE"])

    def print(self):
        click.echo(self.tabulate())


class PullRequestContributionListQuery(GraphQLQuery):
    def __init__(self, dt_from, dt_to, organization=None):
        super().__init__(
            S.PULL_REQUEST_CONTRIBUTION_LIST_STATEMENT,
            pagination_offset=100,
            extra_data={"organization": organization, "from": dt_from.isoformat(), "to": dt_to.isoformat()},
        )
        self.data = []

    def get_count(self):
        return len(self.data)

    def get_pagination_info(self, response):
        return response["data"]["viewer"]["contributionsCollection"]["pullRequestContributions"]["pageInfo"]

    def _handle_response(self, response):
        pr_contributions = response["data"]["viewer"]["contributionsCollection"]["pullRequestContributions"]["edges"]

        for pr_contribution in pr_contributions:
            created = dt_for_str(pr_contribution["node"]["pullRequest"]["createdAt"]).date()
            url = pr_contribution["node"]["pullRequest"]["url"]
            title = shorten_str(pr_contribution["node"]["pullRequest"]["title"])
            self.data.append([created, url, "OWNER", title])

        # Sort by url, then by reversed date:
        self.data = sorted(self.data, key=lambda x: (x[1], x[2], x[3]))
        self.data = sorted(self.data, key=lambda x: x[0], reverse=True)

    def tabulate(self):
        return tabulate(self.data, headers=["CREATED", "PULL REQUEST", "ROLE", "TITLE"])

    def print(self):
        if len(self.data) == 0:
            click.secho("Nothing... 😿 Time to push hard 💪", bold=True)
        else:
            click.echo(self.tabulate())
            click.secho("Count: {}".format(len(self.data)), bold=True)


class PullRequestReviewContributionListQuery(GraphQLQuery):
    def __init__(self, dt_from, dt_to, organization=None):
        super().__init__(
            S.PULL_REQUEST_REVIEW_CONTRIBUTION_LIST_STATEMENT,
            pagination_offset=100,
            extra_data={"organization": organization, "from": dt_from.isoformat(), "to": dt_to.isoformat()},
        )
        self.data = []

    def get_count(self):
        return len(self.data)

    def get_pagination_info(self, response):
        return response["data"]["viewer"]["contributionsCollection"]["pullRequestReviewContributions"]["pageInfo"]

    def _handle_response(self, response):
        rv_contributions = response["data"]["viewer"]["contributionsCollection"]["pullRequestReviewContributions"][
            "edges"
        ]

        for rv_contribution in rv_contributions:
            created = dt_for_str(rv_contribution["node"]["pullRequestReview"]["publishedAt"]).date()
            url = rv_contribution["node"]["pullRequest"]["url"]
            title = shorten_str(rv_contribution["node"]["pullRequest"]["title"])
            self.data.append([created, url, "REVIEWER", title])

        # Sort by url, then by reversed date:
        self.data = sorted(self.data, key=lambda x: (x[1], x[2], x[3]))
        self.data = sorted(self.data, key=lambda x: x[0], reverse=True)

    def tabulate(self):
        return tabulate(self.data, headers=["CREATED", "PULL REQUEST", "ROLE", "TITLE"])

    def print(self):
        if len(self.data) == 0:
            click.secho("Nothing... 😿 Time to push hard 💪", bold=True)
        else:
            click.echo(self.tabulate())
            click.secho("Count: {}".format(len(self.data)), bold=True)


class OneDayContributionListQuery(GraphQLQuery):
    def __init__(self, report_dt):
        super().__init__(S.ONE_DAY_CONTRIBUTION_LIST_STATEMENT, [], extra_data={"date": report_dt.isoformat()})
        self.data = []

    def _handle_response(self, response):
        pr_contributions = response["data"]["viewer"]["contributionsCollection"]["pullRequestContributions"]["edges"]
        rv_contributions = response["data"]["viewer"]["contributionsCollection"]["pullRequestReviewContributions"][
            "edges"
        ]

        for pr_contribution in pr_contributions:
            url = pr_contribution["node"]["pullRequest"]["url"]
            state = pr_contribution["node"]["pullRequest"]["state"]
            self.data.append([url, "OWNER", state])

        for rv_contribution in rv_contributions:
            url = rv_contribution["node"]["pullRequest"]["url"]
            state = rv_contribution["node"]["pullRequestReview"]["state"]
            self.data.append([url, "REVIEWER", state])

        self.data = sorted(self.data, key=lambda x: (x[0], x[1], x[2]))

    def tabulate(self):
        return tabulate(self.data, headers=["PULL REQUEST", "ROLE", "STATE"])

    def print(self):
        click.echo(self.tabulate())


class BranchListQuery(GraphQLQuery):
    def __init__(self, emails=None, is_dangling=False):
        super().__init__(S.BRANCH_LIST_STATEMENT, pagination_offset=10)
        self.data = []
        self.emails = emails
        self.is_dangling = is_dangling

    def get_pagination_info(self, response):
        return response["data"]["viewer"]["repositoriesContributedTo"]["pageInfo"]

    def get_count(self):
        return len(self.data)

    def _handle_response(self, response):
        for repo in response["data"]["viewer"]["repositoriesContributedTo"]["edges"]:
            repo_url = repo["node"]["url"]
            for branch in repo["node"]["refs"]["edges"]:
                branch_name = branch["node"]["name"]
                author_email = branch["node"]["target"]["author"]["email"]
                pr_list = []
                for pr in branch["node"]["associatedPullRequests"]["edges"]:
                    pr_list.append(pr["node"]["url"])
                if self.is_dangling and pr_list:
                    continue
                pr_list = sorted(pr_list)
                if self.emails is not None:
                    if author_email in self.emails:
                        if self.is_dangling:
                            self.data.append([repo_url, branch_name])
                        else:
                            self.data.append([repo_url, branch_name, "\n".join(pr_list)])

        self.data = sorted(self.data, key=lambda x: (x[0], x[1]))

    def print(self):
        no_results_message = "Nothing... 😿 Time to push hard 💪"
        headers = ["REPO", "BRANCH", "PULL REQUEST"]
        if self.is_dangling:
            no_results_message = "Everything is clean 👏"
            headers = ["REPO", "BRANCH"]

        if len(self.data) == 0:
            click.secho(no_results_message, bold=True)
        else:
            click.echo(tabulate(self.data, headers=headers))
            click.secho("Count: {}".format(len(self.data)), bold=True)


class EmailQuery(RESTQuery):
    def __init__(self):
        super().__init__("/user/emails")
        self.emails = None

    def _handle_response(self, response):
        self.emails = [x["email"] for x in response]

    def get_emails(self):
        return self.emails

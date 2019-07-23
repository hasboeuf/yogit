"""
GraphQL queries used by yogit
"""
import click
from tabulate import tabulate

import yogit.api.statements as S
from yogit.api.client import GraphQLClient, RESTClient
from yogit.api.statement import prepare, prepare_pagination
from yogit.utils.dateutils import dt_for_str, days_ago_str
from yogit.utils.spinner import spin


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

    def _get_pagination_info(self):
        raise NotImplementedError()

    @spin
    def execute(self):
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
            pagination_info = self._get_pagination_info(response)
            has_next = pagination_info["hasNextPage"]
            cursor = pagination_info["endCursor"]


class RESTQuery(Query):
    def __init__(self, endpoint):
        super().__init__()
        self.client = RESTClient()
        self.endpoint = endpoint

    @spin
    def execute(self):
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
    def __init__(self):
        super().__init__(S.REVIEW_REQUESTED_STATEMENT, [S.LOGIN_VARIABLE])
        self.data = []

    def _handle_response(self, response):
        for pr in response["data"]["search"]["edges"]:
            repo = pr["node"]["repository"]["nameWithOwner"]
            url = pr["node"]["url"]
            self.data.append([repo, url])
        self.data = sorted(self.data, key=lambda x: x[0])

    def print(self):
        if len(self.data) == 0:
            click.secho("All done! 🎉✨", bold=True)
        else:
            click.echo(tabulate(self.data, headers=["REPO", "URL"]))
            click.secho("Count: {}".format(len(self.data)), bold=True)


class ReviewListQuery(GraphQLQuery):
    def __init__(self):
        super().__init__(S.REVIEW_LIST_STATEMENT, pagination_offset=100)
        self.data = []

    def _get_pagination_info(self, response):
        return response["data"]["viewer"]["contributionsCollection"]["pullRequestReviewContributions"]["pageInfo"]

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
            title = pr["node"]["title"]
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


class OrgaPullRequestListQuery(GraphQLQuery):
    def __init__(self, organization):
        super().__init__(
            S.ORGA_PULL_REQUEST_LIST_STATEMENT, pagination_offset=10, extra_data={"organization": organization}
        )
        self.data = []

    def _get_pagination_info(self, response):
        return response["data"]["search"]["pageInfo"]

    def _handle_response(self, response):
        for pr in response["data"]["search"]["edges"]:
            created = dt_for_str(pr["node"]["createdAt"]).date()
            url = pr["node"]["url"]
            title = pr["node"]["title"]
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


class PullRequestContributionListQuery(GraphQLQuery):
    def __init__(self):
        super().__init__(S.PULL_REQUEST_CONTRIBUTION_LIST_STATEMENT, [S.TODAY_VARIABLE])
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
    def __init__(self, emails=None):
        super().__init__(S.BRANCH_LIST_STATEMENT, pagination_offset=10)
        self.data = []
        self.emails = emails

    def _get_pagination_info(self, response):
        return response["data"]["viewer"]["repositoriesContributedTo"]["pageInfo"]

    def _handle_response(self, response):
        for repo in response["data"]["viewer"]["repositoriesContributedTo"]["edges"]:
            repo_url = repo["node"]["url"]
            for branch in repo["node"]["refs"]["edges"]:
                branch_name = branch["node"]["name"]
                author_email = branch["node"]["target"]["author"]["email"]
                pr_list = []
                for pr in branch["node"]["associatedPullRequests"]["edges"]:
                    pr_list.append(pr["node"]["url"])
                pr_list = sorted(pr_list)
                if self.emails is not None:
                    if author_email in self.emails:
                        self.data.append([repo_url, branch_name, "\n".join(pr_list)])

        self.data = sorted(self.data, key=lambda x: (x[0], x[1]))

    def print(self):
        if len(self.data) == 0:
            click.secho("Nothing... 😿 Time to push hard 💪", bold=True)
        else:
            click.echo(tabulate(self.data, headers=["REPO", "BRANCH", "PULL REQUEST"]))
            click.secho("Count: {}".format(len(self.data)), bold=True)


class EmailQuery(RESTQuery):
    def __init__(self):
        super().__init__("/user/emails")
        self.emails = None

    def _handle_response(self, response):
        self.emails = [x["email"] for x in response]

    def get_emails(self):
        return self.emails

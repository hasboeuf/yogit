"""
GraphQL query statements used by yogit
"""
LOGIN_VARIABLE = "login"
TODAY_VARIABLE = "today"

LOGIN_STATEMENT = """
{
    viewer {
        login
    }
}"""

ORGANIZATION_LIST_STATEMENT = """
{
    viewer {
        organizations(last: 100) {
            edges {
                node {
                    login
                    url
                }
            }
        }
    }
}
"""


REVIEW_REQUESTED_STATEMENT = """
{
    search(query: "type:pr state:$state review-requested:$login", type: ISSUE, first: $offset $after) {
        pageInfo {
            hasNextPage
            endCursor
        }
        edges {
            node {
                ... on PullRequest {
                    updatedAt
                    title
                    number
                    url
                }
            }
        }
    }
}"""


REVIEW_LIST_STATEMENT = """
query {
    viewer {
        contributionsCollection {
            pullRequestReviewContributions(first: $offset $after) {
                pageInfo {
                    hasNextPage
                    endCursor
                }
                edges {
                    node {
                        pullRequestReview {
                            createdAt
                            updatedAt
                            state
                        }
                        pullRequest {
                            url
                            state
                            commits(last:1) {
                                edges {
                                    node {
                                        commit {
                                            pushedDate
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}"""

ORGANIZATION_MEMBER_LIST_STATEMENT = """
query {
    viewer {
        organization(login: $organization) {
            membersWithRole(first: $offset $after) {
                pageInfo {
                    hasNextPage
                    endCursor
                }
                totalCount
                edges {
                    role
                    node {
                        login
                        email
                        location
                    }
                }
            }
        }
    }
}
"""

RATE_LIMIT_STATEMENT = """
{
    rateLimit {
        limit
        cost
        remaining
        resetAt
    }
}
"""


PULL_REQUEST_LIST_STATEMENT = """
{
    viewer {
        pullRequests(first:100, states: OPEN) {
            edges {
                node {
                    createdAt
                    url
                    title
                    mergeable
                }
            }
        }
    }
}
"""

ORGA_PULL_REQUEST_LIST_STATEMENT = """
{
    search(query: "is:open is:pr archived:false user:$organization", type: ISSUE, first: $offset $after) {
        pageInfo {
            hasNextPage
            endCursor
        }
        edges {
            node {
                ... on PullRequest {
                    repository {
                        nameWithOwner
                    }
                    createdAt
                    number
                    url
                    title
                }
            }
        }
    }
}
"""

ONE_DAY_CONTRIBUTION_LIST_STATEMENT = """
{
    viewer {
        contributionsCollection(from: "$date", to: "$date") {
            pullRequestContributions(first: 100) {
                edges {
                    node {
                        pullRequest {
                            url
                            title
                            state
                            createdAt
                            updatedAt
                        }
                    }
                }
            }
            pullRequestReviewContributions(first: 100) {
                edges {
                    node {
                        pullRequestReview {
                            url
                            publishedAt
                            state
                        }
                        pullRequest {
                            url
                        }
                    }
                }
            }
        }
    }
}
"""

PULL_REQUEST_CONTRIBUTION_LIST_STATEMENT = """
{
    viewer {
        contributionsCollection(from: "$from", to: "$to") {
            pullRequestContributions(first: $offset $after) {
                pageInfo {
                    hasNextPage
                    endCursor
                }
                edges {
                    node {
                        pullRequest {
                            url
                            title
                            createdAt
                        }
                    }
                }
            }
        }
    }
}
"""

PULL_REQUEST_REVIEW_CONTRIBUTION_LIST_STATEMENT = """
{
    viewer {
        contributionsCollection(from: "$from", to: "$to") {
            pullRequestReviewContributions(first: $offset $after) {
                pageInfo {
                    hasNextPage
                    endCursor
                }
                edges {
                    node {
                        pullRequestReview {
                            publishedAt
                        }
                        pullRequest {
                            url
                            title
                        }
                    }
                }
            }
        }
    }
}
"""

CONTRIBUTION_STATS_STATEMENT = """
{
    viewer {
        contributionsCollection {
            totalIssueContributions
            totalCommitContributions
            totalRepositoryContributions
            totalPullRequestContributions
            totalPullRequestReviewContributions
            totalRepositoriesWithContributedIssues
            totalRepositoriesWithContributedCommits
            totalRepositoriesWithContributedPullRequests
            totalRepositoriesWithContributedPullRequestReviews
        }
    }
}
"""

BRANCH_LIST_STATEMENT = """
{
    viewer {
        repositoriesContributedTo(first: $offset $after) {
            pageInfo {
                hasNextPage,
                endCursor
            },
            edges {
                node {
                    url
                    refs(first: 100, refPrefix: "refs/heads/") {
                        edges {
                            node {
                                associatedPullRequests(first: 10) {
                                    edges {
                                        node {
                                            url
                                            headRefName
                                        }
                                    }
                                }
                                name
                                target {
                                    ... on Commit {
                                        author {
                                            email
                                            name
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
"""

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
            nodes {
                login
            }
        }
    }
}
"""


REVIEW_REQUESTED_STATEMENT = """
{
    search(query: "type:pr state:open review-requested:$login", type: ISSUE, first: 100) {
        edges {
            node {
                ... on PullRequest {
                    repository {
                        nameWithOwner
                    }
                    number
                    url
                }
            }
        }
    }
}"""

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

PULL_REQUEST_CONTRIBUTION_LIST_STATEMENT = """
{
    viewer {
        contributionsCollection(from: "$today") {
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

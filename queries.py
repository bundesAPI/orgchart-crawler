from gql import gql

ORG_CHART_URLS_QUERY = gql(
    """
    query allOrgChartUrls
     {
      allOrgChartUrls {
        edges {
          node {
            url
            createdAt
            id
            orgchartDocuments {
              edges {
                node {
                  createdAt
                  documentHash
                  status
                }
              }
            }
          }
        }
      }
    }
    """
)
ORG_CHART_URL_QUERY = gql(
    """
    query orgChartUrl($id: ID!) {
  orgChartUrl(id: $id) {
    url
    createdAt
    id
    orgchartDocuments {
      edges {
        node {
          createdAt
          documentHash
          status
        }
      }
    }
  }
}
    """
)

ORG_CHART_CREATE_ERROR = gql(
    """
mutation createOrgChartError($message: String!, $orgChartUrlId: ID!) {
  createOrgChartError(message: $message, orgChartUrlId: $orgChartUrlId) {
    orgChartError {
      message
      id
    }
  }
}
"""
)

ORG_CHART_CREATE = gql(
    """
mutation createOrgChart($document: Upload!, $orgChartUrlId: ID!, $documentHash: String!) {
  createOrgChart(document: $document, orgChartUrlId: $orgChartUrlId, documentHash: $documentHash) {
    orgChart {
      document
    }
    error {__typename}
  }
}
"""
)

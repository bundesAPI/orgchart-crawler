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

ORG_CHART_CREATE_ERROR = gql("""
mutation createOrgChartError($message: String!, $orgChartUrlId: ID!) {
  createOrgChartError(message: $message, orgChartUrlId: $orgChartUrlId) {
    orgChartError {
      message
      id
    }
  }
}
""")
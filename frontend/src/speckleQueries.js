

export const userInfoQuery = `
  query {
    user {
      name
      avatar
    },
    serverInfo {
      name
      company
    }
  }`

export const streamCommitsQuery = `
  query($id: String!, $limit: Int, $cursor: String) {
    stream(id: $id){
      name
      updatedAt
      id
      commits(limit: $limit, cursor: $cursor) {
        totalCount
        cursor
        items{
          id
          message
          branchName
          sourceApplication
          referencedObject
          authorName
          createdAt
        }
      }
    }
  }`

export const streamSearchQuery = `
  query($searchText: String!) {
    streams(query: $searchText) {
      totalCount
      cursor
      items {
        id
        name
        updatedAt
      }
    }
  }`

export const streamObjectQuery = `query($streamId: String!, $objectId: String!) {
    stream(id: $streamId){
        object(id: $objectId){
            data
        }
    }
}`

export const streamBranchesQuery = `query($streamId: String!) {
    stream(id: $streamId){
        branch(name: "main"){
            commits(limit: 1){
                items {
                    referencedObject
                }
            }
        },
        carbonBranch: branch(name: "carbon-results"){
            commits(limit: 1){
                items {
                    referencedObject
                }
            }
        },
        webhooks {
            items{
                url
            }
        }
    }
}`
export default `
query filteredAndPaginatedEvents($offset: Int, $rowsPerPage: Int, $dateGreaterThanEqual: DateTime, $dateLowerThan: DateTime, $labelTextFilter: String) {
  filteredAndPaginatedEvents(offset: $offset, rowsPerPage: $rowsPerPage,  dateGreaterThanEqual: $dateGreaterThanEqual, dateLowerThan: $dateLowerThan, labelTextFilter: $labelTextFilter) {
    filtered
    events {
      addedDate
      confidence
      id
      informedDate
      eventLabel {
        colorGroup
        id
        name
      }
      eventType {
        addedDate
        id
        name
      }
      frames {
        imageUrl
        id
        imageWithBoundingboxesUrl
      }
      inferenceDetectionClassification {
        boundingBoxes {
          bottomRight
          topLeft
          id
        }
      }
      labelsMissing {
        colorGroup
        id
        name
      }
      labelsDetected {
        name
        id
        colorGroup
      }
      keyFrames {
        frames {
          id
          imageWithBoundingboxesUrl
          imageUrl
        }
        id
        name
      }
    }
    typesSummary
    globalTotalNumber
    labelsSummary
    labelTextFilter
    queryTotalNumber
}
}
`

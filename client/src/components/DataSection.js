import React from 'react'

const DataSection = (props) => {
  if (props.title === 'Algorithm Data') {
    return (
      <div>
        <h1>{props.title}</h1>
        <div style={{display:'flex', flexDirection:'column'}}>
          <p>Query: {props.data}s&nbsp;</p>
          <p>User: {props.user}&nbsp;</p>
          <p>MAE: {props.mae}&nbsp;</p>
          <p>RMSE: {props.rmse}</p>
        </div>
      </div>
    )
  } else {
    return (
      <div>
        <h1>{props.title}</h1>
      </div>
    )
  }
}

export default DataSection

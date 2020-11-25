import React from 'react';
import Result from './Result';
import { CircularProgress } from '@material-ui/core';

export default class Results extends React.Component {
  render() {
    if (this.props.loading) {
      return (
        <>
          <div style={{ marginTop: `${this.props.marginTop}` }}>
            <CircularProgress
              size={200}
              thickness={0.5}
              style={{
                visibility: `${this.props.visibility}`,
                display: `${this.props.display}`,
              }}
            />
          </div>
        </>
      );
    } else {
      return (
        <>
          <div>
            {this.props.businesses.map((business) => {
              return <Result business={business} key={business.id} />;
            })}
          </div>
        </>
      );
    }
  }
}

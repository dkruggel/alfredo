import React from 'react';
import Result from './Result';

export default class Results extends React.Component {
  render() {
    return (
      <div>
        {this.props.businesses.map(business => {
          return <Result business={business} key={business.id} />
        })}
      </div>
    );
  }
}

import React from 'react';
import { Button } from '@material-ui/core';

export default class SearchBar extends React.Component {
  constructor(props) {
    super(props);
    this.handleSearch = this.handleSearch.bind(this);
  }

  handleSearch(event) {
    this.props.searchData();
    event.preventDefault();
  }

  render() {
    return (
      <>
        {/* <Input type='text' placeholder='Search...' color='primary'></Input> */}
        {/* <Button color='primary'>Dashboard</Button> */}
        <Button color='primary' onClick={this.handleSearch}>
          Search
        </Button>
      </>
    );
  }
}

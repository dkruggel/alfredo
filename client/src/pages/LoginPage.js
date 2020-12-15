import React from 'react';
import LoginButton from '../components/LoginButton';
import LogoutButton from '../components/LogoutButton';
import SignupButton from '../components/SignupButton';

export const LoginPage = () => {
  return (
    <>
      <LoginButton />
      <SignupButton />
      <LogoutButton />
    </>
  );
};

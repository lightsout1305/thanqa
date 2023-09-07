import { render, screen } from '@testing-library/react';
import App from './App';
import LoginForm from "./components/authentication/LoginForm";

test('TestCasesTable logo is present', () => {
  render(<LoginForm />);
  const ThanQALogo = document.getElementsByClassName("thanqa-logo");
  expect(ThanQALogo).toBeInTheDocument();
});

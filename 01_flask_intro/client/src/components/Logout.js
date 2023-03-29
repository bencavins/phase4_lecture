import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function Logout() {

  const navigate = useNavigate()

  useEffect(() => {
    fetch('/logout', {
      method: 'DELETE'
    })
  }, [])

  return (
    <>
      <h1>You have logged out</h1>
      <a href="/">Back</a>
    </>
  );
}
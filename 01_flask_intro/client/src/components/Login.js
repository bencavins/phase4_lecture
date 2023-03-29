export default function Login({ handleSubmit }) {
  return (
    <div id='login'>
      <h1>Login</h1>
      <form id='login-form' onSubmit={handleSubmit}>
        <label>Username:</label>
        <input type='text' name='username' />
        <label>Password:</label>
        <input type='password' name='password' />
        <input type='submit' />
      </form>
    </div>
  )
}
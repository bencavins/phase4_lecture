export default function Signup({ handleSubmit }) {
  return (
    <div>
      <h1>Sign Up</h1>
      <form id='signup-form' onSubmit={handleSubmit}>
        <label>Username:</label>
        <input type='text' name='username' />
        <label>Email:</label>
        <input type="email" name="email" />
        <label>Password:</label>
        <input type='password' name='password' />
        <input type='submit' />
      </form>
    </div>
  )
}
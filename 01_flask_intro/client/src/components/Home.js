export default function Home({ user }) {
  let content;

  if (user.name) {
    content = <>
      <h2>You are logged in as: {user.name}</h2>
      <a href="/logout">Logout</a>
    </>
  } else {
    content = <a href="/login">Login</a>
  }

  return (
    <div>
      <h1>Home</h1>
      <a href="/signup">Sign Up</a><br />
      { content }<br />
      <a href="/pets">Pets</a>
    </div>
  )
}
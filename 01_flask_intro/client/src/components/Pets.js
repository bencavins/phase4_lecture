export default function Pets({ pets }) {
  return <div>
    <a href="/">Back</a>
    <ul>
      {pets.map(pet => {
        return <li>{pet.name}: {pet.species}</li>
      })}
    </ul>
  </div>
}
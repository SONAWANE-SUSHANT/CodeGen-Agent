import React from 'react';
import ReactDOM from 'react-dom';

class GoaTravelPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      placesToVisit: [
        { name: 'Baga Beach', description: 'A popular beach in North Goa' },
        { name: 'Fort Aguada', description: 'A 17th-century Portuguese fort' },
        { name: 'Dudhsagar Waterfall', description: 'A beautiful waterfall on the Goa-Karnataka border' }
      ],
      thingsToDo: [
        { name: 'Water Sports', description: 'Enjoy water sports like parasailing and jet-skiing' },
        { name: 'Goa Nightlife', description: 'Experience the vibrant nightlife of Goa' },
        { name: 'Goa Cuisine', description: 'Savor the delicious cuisine of Goa' }
      ],
      accommodation: [
        { name: 'Taj Exotica', description: 'A 5-star resort in South Goa' },
        { name: 'The Leela', description: 'A 5-star resort in South Goa' },
        { name: 'Park Hyatt', description: 'A 5-star resort in South Goa' }
      ]
    };
  }

  render() {
    return (
      <div>
        <header id="header">
          <h1>Goa Travel Page</h1>
        </header>
        <main id="main">
          <div id="map-view" className="container">
            <h2>Map View</h2>
            <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3834.902111101794!2d73.77765431499999!3d15.299327289999998!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bbfc14b5c64e991%3A0x6bd24c45c75c6f3!2sGoa%2C+India!5e0!3m2!1sen!2sin!4v1558771713555!5m2!1sen!2sin" width="600" height="450" frameBorder="0" style={{ border: 0 }} allowFullScreen></iframe>
          </div>
          <section id="places-to-visit">
            <h2>Places to Visit</h2>
            <ul>
              {this.state.placesToVisit.map((place, index) => (
                <li key={index}>
                  <h3>{place.name}</h3>
                  <p>{place.description}</p>
                </li>
              ))}
            </ul>
          </section>
          <section id="things-to-do">
            <h2>Things to Do</h2>
            <ul>
              {this.state.thingsToDo.map((thing, index) => (
                <li key={index}>
                  <h3>{thing.name}</h3>
                  <p>{thing.description}</p>
                </li>
              ))}
            </ul>
          </section>
          <section id="accommodation">
            <h2>Accommodation</h2>
            <ul>
              {this.state.accommodation.map((accommodation, index) => (
                <li key={index}>
                  <h3>{accommodation.name}</h3>
                  <p>{accommodation.description}</p>
                </li>
              ))}
            </ul>
          </section>
        </main>
        <footer id="footer">
          <p>&copy; 2024 Goa Travel Page</p>
        </footer>
      </div>
    );
  }
}

ReactDOM.render(<GoaTravelPage />, document.getElementById('main'));
describe('R8UC3', () => {
  // define variables that we need on multiple occasions
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user

  before(function () {
    // create a fabricated user from a fixture
    cy.fixture('user.json')
      .then((user) => {
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/users/create',
          form: true,
          body: user
        }).then((response) => {
          uid = response.body._id.$oid
          name = user.firstName + ' ' + user.lastName
          email = user.email

        })
      })
  })

  beforeEach(function () {
    // enter the main main page
    cy.visit('http://localhost:3000')

    // login
    cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email)

    cy.get('form')
      .submit()

  })



  it('when user clickes x beside the todo the todo item should be removed.', () => {
    // Create task
    cy.get("input[id='title']").type("Cypress");
    cy.get("input[id='url']").type("BQqzfHQkREo{enter}");

    // Detailed view
    cy.get(".title-overlay").contains("Cypress").parent().click();

    // Create todo
    cy.get(".inline-form input[placeholder='Add a new todo item']").type("Make notes", {force: true});
    cy.get(".inline-form input[type='submit']").click({force: true});


    cy.contains(".todo-list li", "Make notes").find(".remover").click();
    cy.contains(".todo-list li", "Make notes").should("not.exist");
  })


  after(function () {
    // clean up by deleting the user from the database
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })
})
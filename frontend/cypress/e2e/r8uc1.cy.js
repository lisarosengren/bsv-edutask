describe('R8UC1', () => {
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

  it('add button not disabled if description is typed', () => {
    
    // Create task
    cy.get("input[id='title']").type("Cypress");
    cy.get("input[id='url']").type("BQqzfHQkREo{enter}");

    // detailed view
    cy.get(".title-overlay").contains("Cypress").parent().click();

    // Type description
    cy.get(".inline-form input[placeholder='Add a new todo item']").type("Make cake", {force: true});
    cy.get(".inline-form input[type='submit']").should('not.be.disabled');
  })

  it('new, active, todo item added to the bottom of the list', () => {

    // Create task
    cy.get("input[id='title']").type("Cypress 2");
    cy.get("input[id='url']").type("BQqzfHQkREo{enter}");

    // detailed view
    cy.get(".title-overlay").contains("Cypress 2").parent().click();

    cy.get(".inline-form input[placeholder='Add a new todo item']").type("Make notes", {force: true});
    cy.get(".inline-form input[type='submit']").click({force: true});

    cy.get('.todo-list li[class="todo-item"]').last().should("contain", "Make notes");
    cy.contains(".todo-list li", "Make notes").find(".checker").should("have.class", "unchecked");
  })


  it('when description is empty from start the add button should be disabled', () => {
    // Create task
    cy.get("input[id='title']").type("Cypress 3");
    cy.get("input[id='url']").type("BQqzfHQkREo{enter}");

    // detailed view
    cy.get(".title-overlay").contains("Cypress 3").parent().click();


    cy.get(".inline-form input[type='submit']").should('be.disabled');
  })

  it('when description is typed and deleted the add button should be disabled', () => {
    // Create task
    cy.get("input[id='title']").type("Cypress 4");
    cy.get("input[id='url']").type("BQqzfHQkREo{enter}");

    // detailed view
    cy.get(".title-overlay").contains("Cypress 4").parent().click();

    cy.get(".inline-form input[placeholder='Add a new todo item']").type("M{backspace}", {force: true});
    cy.get(".inline-form input[type='submit']").should('be.disabled');
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
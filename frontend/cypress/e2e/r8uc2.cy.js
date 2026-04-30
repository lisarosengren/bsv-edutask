describe('R8UC2', () => {
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
  
  it('when todo icon is clicked and it did not have the class checked it should be checked and be struck out.', () => {

    // Create task
    cy.get("input[id='title']").type("Cypress");
    cy.get("input[id='url']").type("BQqzfHQkREo{enter}");

    // Detailed view
    cy.get(".title-overlay").contains("Cypress").parent().click();

    // Create todo
    cy.get(".inline-form input[placeholder='Add a new todo item']").type("Make notes", {force: true});
    cy.get(".inline-form input[type='submit']").click({force: true});


    cy.contains(".todo-list li", "Make notes").find(".checker").click();
    cy.contains(".todo-list li", "Make notes").find(".checker").should("have.class", "checked");
    cy.contains(".todo-list li", "Make notes").find(".editable").invoke('css', 'text-decoration').should('contain', 'line-through');
  })
  
  it('when todo icon is clicked when it was already checked before it should have correct class and not be struck out.', () => {
    
    // Create task
    cy.get("input[id='title']").type("Cypress 2");
    cy.get("input[id='url']").type("BQqzfHQkREo{enter}");

    // Detailed view
    cy.get(".title-overlay").contains("Cypress 2").parent().click();

    // Create todo
    cy.get(".inline-form input[placeholder='Add a new todo item']").type("Make notes", {force: true});
    cy.get(".inline-form input[type='submit']").click({force: true});
    
      
    
    // Check todo
    cy.contains(".todo-list li", "Make notes").find(".checker").click();

    // click checked todo
    cy.contains(".todo-list li", "Make notes").find(".checker").click({force: true});
    cy.contains(".todo-list li", "Make notes").find(".checker").should("have.class", "unchecked");
    cy.contains(".todo-list li", "Make notes").find(".editable").invoke('css', 'text-decoration').should('not.contain', 'line-through');
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
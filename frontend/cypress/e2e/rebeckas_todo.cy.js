describe('Logging into the system', () => {
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

  it('The user enters a description of a todo item into an empty input form field.', () => {
    cy.get("input[id='title']").type("Cypress");
    cy.get("input[id='url']").type("BQqzfHQkREo{enter}");

    cy.get(".title-overlay").contains("Cypress").parent().click();

    cy.get(".inline-form input[placeholder='Add a new todo item']").type("Make notes", {force: true});
    cy.get(".inline-form input[type='submit']").click({force: true});

    cy.get('.todo-list li[class="todo-item"').last().should("contain", "Make notes");
  })

  it('when description is empty the add button should be disabled', () => {
    cy.get(".title-overlay").contains("Cypress").parent().click();
    cy.get(".inline-form input[type='submit']").should('be.disabled');
  })

  it('when todo is checked it should have correct class and be struck out.', () => {
    cy.get(".title-overlay").contains("Cypress").parent().click();
    cy.contains(".todo-list li", "Make notes").find(".checker").click();
    cy.contains(".todo-list li", "Make notes").find(".checker").should("have.class", "checked");
    cy.contains(".todo-list li", "Make notes").find(".editable").invoke('css', 'text-decoration').should('contain', 'line-through');
    cy.contains(".todo-list li", "Make notes").find(".checker").click();
  })
  
  it('when todo is checked when it was already checked before it should have correct class and not be struck out.', () => {
    cy.get(".title-overlay").contains("Cypress").parent().click();
    cy.contains(".todo-list li", "Make notes").find(".checker").click();
    cy.contains(".todo-list li", "Make notes").find(".checker").should("have.class", "checked");
    cy.contains(".todo-list li", "Make notes").find(".checker").click();
    cy.contains(".todo-list li", "Make notes").find(".checker").should("have.class", "unchecked");
    cy.contains(".todo-list li", "Make notes").find(".editable").invoke('css', 'text-decoration').should('not.contain', 'line-through');
  })

  it('when user clickes x beside the todo it the todo item should be removed.', () => {
    cy.get(".title-overlay").contains("Cypress").parent().click();
    cy.contains(".todo-list li", "Make notes").find(".remover").click();
    // problem: If x is clicked and then imediatly check if it does not exist its not removed, but if you check something else it has time(?) to remove.
    cy.get('h1')
      .should('contain.text', 'Your tasks, ' + name)
    
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
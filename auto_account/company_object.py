class company():
      def __init__(self,id,name,legal_form,state,employees=None) -> None:
          self.id=id
          self.name=name
          self.active=True
          self.link=""
          self.html=""
          self.dict={"id":self.id,"status":self.active}
          self.legal_form=legal_form
          self.state=state
          self.employees=employees
          self.annual_accounts={}
      def __str__(self) -> str:
            return self.name



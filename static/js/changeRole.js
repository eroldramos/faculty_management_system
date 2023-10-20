async function changeRole(id, num, department){

  console.log(id, num, department)
    const response = await fetch(`/change-role/${id}/${num}/${department}`, {
      method: "GET",
      // body:  {
      //     csrfmiddlewaretoken : document.getElementsByName('csrfmiddlewaretoken')[0].value,
      //   },
      headers: {
        "Content-Type": "application/json",
      },
      credentials: 'same-origin'
    });
    
    if (!response.ok) {
      alert('Something went wrong!')
      // console.log(response.json())
      return
    }
    //if dont receive error
    // const data = await response.json();
    
    window.location.reload()
    
      }
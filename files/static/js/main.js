    function delete_img(id){
        let response = await fetch('image/'+id+'/delete');

        if (response.ok) {
          let json = await response.json();
          console.log("Good");
        } else {
          alert("Ошибка HTTP: " + response.status);
        }
    }

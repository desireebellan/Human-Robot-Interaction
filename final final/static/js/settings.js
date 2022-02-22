var Color = document.forms['setting']['backSet'];
var color = 'red'
function changeColor(){
		document.body.style.background = color;
		Color.setAttribute('class','button '+color+'Pallette')
		if (color == 'red'):
			color = 'blue'
				
	}

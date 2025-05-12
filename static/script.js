function shiftChar(char, shift) {
    if (/[^a-zA-Z]/.test(char)) return char;
    const code = char.charCodeAt(0);
    const base = code <= 90 ? 65 : 97;
    return String.fromCharCode(((code - base + shift) % 26 + 26) % 26 + base);
  }
  
  function animarTransformacion(mensaje, shift) {
    const output = document.getElementById('output');
    output.innerHTML = '';
    
    if (!mensaje) {
      output.innerHTML = '<p style="color: #6c757d;">Tu animación aparecerá aquí...</p>';
      return;
    }
    
    mensaje.split('').forEach((char, index) => {
      const container = document.createElement('div');
      container.className = 'char-container';
      
      const arrow = document.createElement('div');
      arrow.className = 'arrow';
      arrow.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 15a.5.5 0 0 0 .5-.5V2.707l3.146 3.147a.5.5 0 0 0 .708-.708l-4-4a.5.5 0 0 0-.708 0l-4 4a.5.5 0 1 0 .708.708L7.5 2.707V14.5a.5.5 0 0 0 .5.5z"/></svg>';
      
      const charBox = document.createElement('div');
      charBox.className = 'char-box';
      charBox.textContent = char;
      
      const indicator = document.createElement('div');
      indicator.className = 'step-indicator';
      
      container.appendChild(arrow);
      container.appendChild(charBox);
      container.appendChild(indicator);
      output.appendChild(container);
  
      // Animación por pasos
      for (let step = 1; step <= shift; step++) {
        setTimeout(() => {
          // Actualizar letra
          charBox.textContent = shiftChar(char, step);
          charBox.style.transform = 'scale(1.1)';
          charBox.style.background = '#e3f2fd';
          charBox.style.borderColor = 'var(--accent)';
          charBox.style.boxShadow = '0 0 10px rgba(67, 97, 238, 0.2)';
          
          // Actualizar indicador
          indicator.textContent = `+${step}`;
          
          // Animación de flecha
          arrow.style.animation = 'move 0.5s';
          setTimeout(() => {
            arrow.style.animation = '';
            charBox.style.transform = '';
            charBox.style.background = '';
            charBox.style.borderColor = '';
            charBox.style.boxShadow = '';
          }, 300);
        }, index * 200 + step * 200);
      }
    });
  }
  
  async function enviar() {
    const mensaje = document.getElementById('input').value.trim();
    const shift = 3;
    
    // Actualizar UI
    document.getElementById('original-value').textContent = mensaje || '-';
    document.getElementById('cifrado-value').textContent = '-';
    
    const statusElement = document.getElementById('status-message');
    statusElement.innerHTML = '<div class="status-message"><span class="loading"></span> Procesando mensaje...</div>';
    
    if (!mensaje) {
      statusElement.innerHTML = '<div class="status-message error">Por favor ingresa un mensaje</div>';
      animarTransformacion('', shift);
      return;
    }
    
    // Mostrar animación
    animarTransformacion(mensaje, shift);
    
    try {
      const response = await fetch('/cifrar', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ mensaje: mensaje })
      });
  
      const data = await response.json();
      
      if (data.status === 'success') {
        document.getElementById('cifrado-value').textContent = data.cifrado;
        statusElement.innerHTML = '<div class="status-message success">Mensaje cifrado y guardado correctamente</div>';
      } else {
        statusElement.innerHTML = `<div class="status-message error">Error: ${data.message || 'Error desconocido'}</div>`;
      }
    } catch (error) {
      console.error('Error:', error);
      statusElement.innerHTML = '<div class="status-message error">Error al comunicarse con el servidor</div>';
    }
  }
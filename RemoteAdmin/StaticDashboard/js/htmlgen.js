// Global context to store selected template type
var TEMPLATE_TYPE_ID = 0;

templates = [
  `<h1>[template-headline]</h1>
  <h3>[template-content]</h3>`,

  `<div class="flex-provider">
    <h1>[template-headline]</h1>
    <img src="uploads/[template-content]" alt="" class="smart-image">
  </div>`
]


function generateHTML(type_id) {
  let template = templates[type_id];
  let final = templates[type_id];

  // Get currently active template input container
  let data_node = document.getElementById('html-editor-values')
    .children[type_id];

  // Find all data replacement points
  let isReplacementId = false;
  let replacementId = ''
  for (var i = 0; i < template.length; i++) {
    let char = template[i];

    if (char == '[') { // starting replacement indicator
      isReplacementId = true; // set accumulation flag
    } else if (isReplacementId && char == ']') { // ending replacement indicator
      isReplacementId = false; // reset accumulation flag
      // replace expression with data from user
      final = final.replace('[' + replacementId + ']', data_node.getElementsByClassName(replacementId)[0]
        .innerText);
      // reset number buffer
      replacementId = '';
    } else if (isReplacementId) {
      replacementId += char; // if flag is set: add digit to buffer
    }
  }
  return final;
}

function openTemplatingEditor() {
  document.getElementById('templating-main')
    .classList.remove('hidden');
}

function htmlEditorSave() {
  let html = generateHTML(TEMPLATE_TYPE_ID);
  document.getElementById('templating-main')
    .classList.add('hidden');
  document.getElementById('node-content-raw')
    .innerText = html;
}


function selectPresetType(type_id) {
  TEMPLATE_TYPE_ID = type_id;
  let type_buttons = document.getElementById('templating-presets')
    .children;
  let templating_inputs = document.getElementById('html-editor-values')
    .children;
  for (var i = 0; i < type_buttons.length - 1; i++) {
    type_buttons[i].classList.remove('htmltype-selected');
    templating_inputs[i].classList.add('hidden');
  }
  type_buttons[type_id].classList.add('htmltype-selected');
  templating_inputs[type_id].classList.remove('hidden');
}

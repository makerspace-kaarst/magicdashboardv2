# DOCUMENTAION: NodeMagic

> This is the official documentation about the administration panel of the MagicDashboard, which controls the text and image display of the MagicMirror.

**Topics**

- [Get started](#get-started)
- [Add a node and add slices](#add-a-node-and-add-slices)
- [Edit a slice with the "Node Templating Editor"](#edit-a-slice-with-the-node-templating-editor)
- [Remove a node or a slice](#remove-a-node-or-a-slice)
- [Changing the duration of the slices](#changing-the-duration-of-the-slices)
- [Upload an image](#upload-an-image)
- [License](#license)

## Get started

> Here you can see the login data, which you need to log in at the admin panel.

### Step 1

- Open the Panel using "index.html" in your preferred browser.

### Step 2

- Log in with the following login data:
  - Server-IP: ***192.168.178.107***
  - Port: ***1337***
  - API-Key: ***ChangeMe***

---

## Add a node and add slices

- To create a node with the NodeMagic editor, click the "Add a node" button at the bottom left.

  ![Add a node](img/add_a_node.png)

- After creating the node you can create different slices with the green "+" button and [then you can edit them with the "Node Templating Editor"](#edit-a-slice-with-the-node-templating-editor).

  ![Add a slice](img/add_a_slice.png)

---

## Edit a slice with the "Node Templating Editor"

- After creating a slice, you can open it by clicking on the created slice.

  ![Click on a slice](img/click_on_a_slice.png)

- Then you can click on the "Open node templating editor" button to open the HTML generator for the slice.

  ![Open node templating editor](img/open_node_templating_editor.png)

- There are then different selection options, which can then be changed according to the desired operation.

  ![Click on a slice](img/click_on_a_slice.png)

- When you have selected and filled out the desired option, you can click on "Save" above and then confirm the generated HTML text again with "Save".

  ![Save](img/save.png)

---

## Remove a node or a slice

### Remove a node

- To remove a node, after you have selected the desired node, click on the "Delete Node" button, which can be seen at the top center of the page.

  ![Delete a node](img/delete_a_node.png)

### Remove a slice

- If you want to remove a slice, press the "-" button under the desired slice.

  ![Delete a slice](img/delete_a_slice.png)

---

## Changing the duration of the slices

- The editing of the duration between slices changes can be set using the text field in the upper-center area.
- There you can set in seconds how long the time between the changes is.

  ![Changing the duration of the slices](img/changing_the_duration_of_the_slices.png)

---

## Upload an image

- To add an image in the "Node Templating Editor", you need to add the desired image in the main menu under "Upload an image" at the bottom left.

  ![Upload an image](img/upload_an_image.png)

- After uploading the image, you can insert the image into a slice using the "Node Templating Editor". To do this, you need a headline and the file name of the image (for example: "img001.png").

***ATTENTION:*** The uploader can only process PNG and JPEG files. Other files will be uploaded, but you cannot use them.

---

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2020 © <a href="http://makerspace.jh220.de" target="_blank">Makerspace Kaarst</a>.

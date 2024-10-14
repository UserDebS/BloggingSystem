import './App.css';
import { useRef } from 'react';
import ReactQuill, { Quill } from 'react-quill';
import 'react-quill/dist/quill.snow.css';
import { Button } from './components/ui/button';

const Block = Quill.import('blots/block');
class NoteBlock extends Block {
  static blotName = 'note';
  static tagName = 'div';
  static className = 'note-format'
}

Quill.register(NoteBlock);

Quill.import('ui/icons')['note'] = `
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="note-icon">
<mask id="mask0_2_10" style="mask-type:alpha" maskUnits="userSpaceOnUse" x="0" y="0" width="24" height="24">
<rect width="24" height="24" fill="#D9D9D9"/>
</mask>
<g mask="url(#mask0_2_10)">
<path d="M17.5 18.5V20.5C17.5 20.6333 17.55 20.75 17.65 20.85C17.75 20.95 17.8667 21 18 21C18.1333 21 18.25 20.95 18.35 20.85C18.45 20.75 18.5 20.6333 18.5 20.5V18.5H20.5C20.6333 18.5 20.75 18.45 20.85 18.35C20.95 18.25 21 18.1333 21 18C21 17.8667 20.95 17.75 20.85 17.65C20.75 17.55 20.6333 17.5 20.5 17.5H18.5V15.5C18.5 15.3667 18.45 15.25 18.35 15.15C18.25 15.05 18.1333 15 18 15C17.8667 15 17.75 15.05 17.65 15.15C17.55 15.25 17.5 15.3667 17.5 15.5V17.5H15.5C15.3667 17.5 15.25 17.55 15.15 17.65C15.05 17.75 15 17.8667 15 18C15 18.1333 15.05 18.25 15.15 18.35C15.25 18.45 15.3667 18.5 15.5 18.5H17.5ZM5 21C4.45 21 3.97917 20.8042 3.5875 20.4125C3.19583 20.0208 3 19.55 3 19V5C3 4.45 3.19583 3.97917 3.5875 3.5875C3.97917 3.19583 4.45 3 5 3H19C19.55 3 20.0208 3.19583 20.4125 3.5875C20.8042 3.97917 21 4.45 21 5V10C21 10.2833 20.9042 10.5208 20.7125 10.7125C20.5208 10.9042 20.2833 11 20 11C19.7167 11 19.4792 10.9042 19.2875 10.7125C19.0958 10.5208 19 10.2833 19 10V5H5V19H10C10.2833 19 10.5208 19.0958 10.7125 19.2875C10.9042 19.4792 11 19.7167 11 20C11 20.2833 10.9042 20.5208 10.7125 20.7125C10.5208 20.9042 10.2833 21 10 21H5ZM5 19V5V11.075V11V19ZM7 16C7 16.2833 7.09583 16.5208 7.2875 16.7125C7.47917 16.9042 7.71667 17 8 17H10.075C10.3583 17 10.5958 16.9042 10.7875 16.7125C10.9792 16.5208 11.075 16.2833 11.075 16C11.075 15.7167 10.9792 15.4792 10.7875 15.2875C10.5958 15.0958 10.3583 15 10.075 15H8C7.71667 15 7.47917 15.0958 7.2875 15.2875C7.09583 15.4792 7 15.7167 7 16ZM7 12C7 12.2833 7.09583 12.5208 7.2875 12.7125C7.47917 12.9042 7.71667 13 8 13H13C13.2833 13 13.5208 12.9042 13.7125 12.7125C13.9042 12.5208 14 12.2833 14 12C14 11.7167 13.9042 11.4792 13.7125 11.2875C13.5208 11.0958 13.2833 11 13 11H8C7.71667 11 7.47917 11.0958 7.2875 11.2875C7.09583 11.4792 7 11.7167 7 12ZM7 8C7 8.28333 7.09583 8.52083 7.2875 8.7125C7.47917 8.90417 7.71667 9 8 9H16C16.2833 9 16.5208 8.90417 16.7125 8.7125C16.9042 8.52083 17 8.28333 17 8C17 7.71667 16.9042 7.47917 16.7125 7.2875C16.5208 7.09583 16.2833 7 16 7H8C7.71667 7 7.47917 7.09583 7.2875 7.2875C7.09583 7.47917 7 7.71667 7 8ZM18 23C16.6167 23 15.4375 22.5125 14.4625 21.5375C13.4875 20.5625 13 19.3833 13 18C13 16.6167 13.4875 15.4375 14.4625 14.4625C15.4375 13.4875 16.6167 13 18 13C19.3833 13 20.5625 13.4875 21.5375 14.4625C22.5125 15.4375 23 16.6167 23 18C23 19.3833 22.5125 20.5625 21.5375 21.5375C20.5625 22.5125 19.3833 23 18 23Z" fill="black"/>
</g>
</svg>
`;

const modules: Readonly<any> = {
  toolbar: {
    container: [
      [{ 'header': [1, 2, 3, false] }],
      ['bold', 'italic', 'underline', 'strike'],
      [{ 'list': 'ordered' }, { 'list': 'bullet' }],
      ['link', 'image'],
      ['note']
    ],
    handler: {
      'note': function () {
        const quill = this.quill;
        const range = this.getSelection();
        if (range) {
          quill.format('note', 'true');
        }
      }
    }
  }
};

function App() {
  const quillValue = useRef<any>(null);
  const quillText = useRef<string>('');
  const saveTimeout = useRef<NodeJS.Timeout | null>(null);

  const handleClick = async () => {
    const res = await fetch('/upload',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          'quillData': {
            'title': 'quill',
            'content': quillValue.current,
            'tags': ['coding', 'web dev', 'ai'],
          },
          'text': quillText.current
        })
      }
    ).then(result => result.json())
      .catch(_ => console.log(_));
    console.log(res);
  }

  const handleChange = (_value: any, _delta: any, _source: any, editor: any) => {
    quillValue.current = editor.getContents();
    quillText.current = editor.getText();
    if (saveTimeout.current) {
      clearTimeout(saveTimeout.current);
    }

    saveTimeout.current = setTimeout(() => {
      if (quillValue.current) {
        console.log({
          'title': 'quill',
          'content': quillValue.current,
          'tags': ['this', 'is', 'hard'],
          'text': quillText.current
        });
      }
    }, 300);
  }
  return (
    <>
      <ReactQuill theme='snow' value={quillValue.current} onChange={handleChange} modules={modules} />
      <Button onClick={handleClick}>Click me</Button>
    </>
  )
}

export default App

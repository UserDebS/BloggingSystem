import { note } from '@/svgs/Svgs';
import React, { useRef, useState } from 'react';
import ReactQuill, {Quill} from 'react-quill';
import ImageResize from 'quill-image-resize-module-react';
import 'react-quill/dist/quill.snow.css'
import '@/App.css'
import { Input } from './input';
import { Content } from '@/lib/types';
import { read } from 'fs';
import { Button } from './button';

class NoteBlock extends Quill.import('blots/block'){
    static blotName = 'note';
    static tagName = 'div';
    static className = 'note-block'
}

class CustomQuill extends Quill{}

interface QuillModules {
    toolbar : {
        container : Array<Array<object | string>>;
        handlers : {
            [key : string] : (this : CustomQuill) => void
        }
    }, 
    imageResize : {
        [key : string] : any
    }
}

const customIcon = Quill.import('ui/icons');

customIcon['note'] = note;

Quill.register(NoteBlock, true);
Quill.register('modules/imageResize', ImageResize);

const Editor = ({readOnly = false, fetchedContent = null} : {readOnly : boolean; fetchedContent : Readonly<Content> | null}) => {
    const MemoizedEditor = React.memo(ReactQuill);
    const editorRef = useRef<any>(fetchedContent);
    const contentRef = useRef<string>('');
    const contentTitle = useRef<string>('');
    const tagName = useRef<string>('');
    const [tagList, setTagList] = useState<string[]>([]);
    const modules: Readonly<QuillModules> = {
        toolbar: {
            container: [
                [{ 'header': '1' }, { 'header': '2' }, { 'font': [] }],
                [{ 'list': 'ordered' }, { 'list': 'bullet' }],
                ['bold', 'italic', 'underline', 'strike', 'blockquote'],
                ['link', 'image', 'note'],
            ],
            handlers : {
                'note' : function(this : CustomQuill) {
                    const quill = this.quill;
                    const range = quill.getSelection();
                    if(range) {
                        const currentFormat = quill.getFormat(range);
                        const isNoteActive = currentFormat.note;
                        quill.format('note', !isNoteActive);
                    }
                }
            }
        },
        imageResize : {
            parchment: Quill.import('parchment'),
            modules: ['Resize', 'DisplaySize']
        }
    }

    const handleChange = (_value : string, _delta : any, _src : any, editor : ReactQuill.UnprivilegedEditor) => {
        editorRef.current = editor.getContents();
        contentRef.current = editor.getText();
        console.log(contentTitle.current);
        console.log(editorRef.current);
        console.log(contentRef.current);
        console.log(tagList);
        requestHandler();
    }

    const selectionChange = (_selection : ReactQuill.Range, _src : any, editor : ReactQuill.UnprivilegedEditor) => {
        editorRef.current = editor.getContents();
        contentRef.current = editor.getText();
        console.log(contentTitle.current);
        console.log(editorRef.current); 
        console.log(contentRef.current);
        console.log(tagList); 
    }

    const handleListInput = () => {
        if(tagName.current.length == 0) return;
        setTagList(prev => [...prev, tagName.current]);
    }

    return (
        <div className={'blog-editor p-2 w-full h-full [&_.ql-container]:rounded-b-[5px] [&_.ql-toolbar]:rounded-t-[5px] ' + (readOnly? ' [&_.ql-toolbar]:hidden [&_.ql-container]:rounded-t-[5px] read-only-editor' : '')}>
            {
                !readOnly?<>
                    <label className='font-bold' htmlFor="title">Title</label>
                    <Input 
                        onChange={e => contentTitle.current = e.currentTarget.value} 
                        id='title'
                        className='rounded h-10 mb-2 placeholder:capitalize' 
                        placeholder='Enter your Title' 
                    />
                </> : <h1 className='blog-header font-bold text-4xl my-2'>{fetchedContent?.title ?? 'Looks like the owner of this blog does not like titles...'}</h1>
            }
            <MemoizedEditor 
                readOnly = {readOnly}
                modules={modules}
                theme='snow'
                value={readOnly? editorRef.current : fetchedContent?.content}
                onChange={handleChange}
                onChangeSelection={selectionChange}
                placeholder="Let's write something epic!!!"
            />

            <label className='font-bold' htmlFor="taglist">Tag List</label>
            {
                !readOnly?
                <Input 
                onChange={e => {tagName.current = e.currentTarget.value;}} 
                onKeyUp={e => {
                    if(e.key.toUpperCase() == 'ENTER') handleListInput();
                }} 
                id='taglist' 
                className='rounded-t-[5px] h-10 border-b-0 placeholder:capitalize' 
                placeholder='Enter tags for better search(Press Enter to add it)'
                /> :
                ''
            }
            <div className='rounded-b-[5px] border-[1px] p-1 border-black flex w-full gap-1 min-h-1 flex-wrap'>
                {!readOnly?tagList.map((tag, index) => 
                    <div key={index} onClick={_ => setTagList(tagList.filter((_, ind) => ind != index))} className='list-items px-2 py-2 border-2 font-semibold rounded border-black inline-block cursor-pointer relative hover:border-red-500 hover:before:content-["❌"]  hover:text-red-800 hover:bg-red-400'>
                        {tag}
                    </div>
                ) : fetchedContent?.tags.map((tag, index) => <div key={index} className='list-items px-2 py-2 border-2 font-semibold rounded border-black inline-block'>
                {tag}
            </div>)}
            </div>
            {
                readOnly?
                '':
                <Button className='my-1 bg-black text-white rounded hover:bg-slate-700' onClick={_=>null}>POST</Button>
            }
        </div>
    )
}

export default Editor;
import { FileDrop } from "react-file-drop"

import { upload_file } from "@/lib/api"
import { delay } from "@/lib/utils"

export function Add() {
  const handleDropped = (droppedFiles: FileList) => {
    upload_file(droppedFiles)
      .then(() => delay(2000))
      .then(() => window.location.reload())
  }

  return (
    <div className='z-50 w-40 h-40 m-2 border-4 border-dashed bg-gray-100 rounded bg-opacity-50 cursor-pointer group hover:bg-opacity-90 hover:z-20 duration-200'>
      <FileDrop
        className='w-40 h-40 py-2 pr-2 flex flex-col items-center justify-center'
        onDrop={(files: FileList | null) => handleDropped(files!)}>
        <p className='text-center text-lg uppercase'>Drop Files Here!</p>
        <svg
          className='w-8 h-8 mx-auto my-6 rotate-45 text-blue-500 group-hover:rotate-[135deg] group-hover:text-lime-500 duration-200'
          fill='currentColor'
          viewBox='7 2 10 20'
          xmlns='http://www.w3.org/2000/svg'>
          <path d='M13.41 12l4.3-4.29a1 1 0 1 0-1.42-1.42L12 10.59l-4.29-4.3a1 1 0 0 0-1.42 1.42l4.3 4.29-4.3 4.29a1 1 0 0 0 0 1.42 1 1 0 0 0 1.42 0l4.29-4.3 4.29 4.3a1 1 0 0 0 1.42 0 1 1 0 0 0 0-1.42z'></path>
        </svg>
        <p className='text-center text-xs mb-2'>
          Refresh page for the new list of files after upload.
        </p>
      </FileDrop>
    </div>
  )
}

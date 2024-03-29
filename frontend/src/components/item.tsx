import { useState } from "react"
import { FileCode2, FileText } from "lucide-react"

import { FileInfoProps } from "@/types"
import { cn, formatBytes, delay } from "@/lib/utils"

type ItemProps = {
  params: FileInfoProps
  handleSelect: (id: string) => void
}

export function Item({ params, handleSelect }: ItemProps) {
  const [isCopied, setIsCopied] = useState(false)

  const image_base = import.meta.env.VITE_BASE_URL
  const image_path = `${image_base}/get/${params.id}/`
  const days = Math.floor(params.delta_time / 86400)
  const file_size = formatBytes(params.size)
  const isImage = params.filename.match(/\.(jpg|jpeg|png|gif)$/i)
  const isPDF = params.filename.match(/\.(pdf)$/i)

  if (!params.selected) params.selected = false

  const copyText = (text: string) => {
    navigator.clipboard.writeText(text)
    setIsCopied(true)
    delay(2000).then(() => setIsCopied(false))
  }

  return (
    <div
      className={cn(
        "flex flex-col rounded-lg shadow-md text-zinc-700 text-xs m-2 p-2 w-72 hover:scale-105 transition-transform",
        params.selected ? "bg-zinc-300/50" : "bg-white"
      )}>
      {isImage && (
        <img
          src={image_path}
          alt={params.filename}
          width={320}
          className='w-fit'
        />
      )}
      {isPDF && <FileText className='w-20 h-20 mx-auto' />}
      {!isImage && !isPDF && <FileCode2 className='w-20 h-20 mx-auto' />}
      <p className='overflow-hidden text-ellipsis hover:overflow-visible'>
        Filename:
        <code className='bg-zinc-200 px-1 rounded'>{params.filename}</code>
      </p>
      <p className='w-64 overflow-hidden text-ellipsis hover:overflow-visible'>
        url:
        <code
          className={cn(
            "px-1 rounded",
            isCopied ? "bg-emerald-300 " : "bg-zinc-200"
          )}
          onClick={() => copyText(image_path)}>
          {image_path}
        </code>
      </p>
      <p>
        Size:
        <code className='bg-zinc-200 px-1 rounded'>{file_size}</code>
      </p>
      <p>
        Exsist time:
        <code className='bg-zinc-200 px-1 rounded'>{days} days</code>
      </p>
      <p>
        <a href={`${image_path}?output=download`} target='_blank'>
          <button className='rounded h-5 mt-1 bg-sky-200 hover:bg-orange-300 px-2'>
            Download
          </button>
        </a>
        <input
          type='checkbox'
          id={params.id}
          name={params.id}
          checked={params.selected}
          onChange={() => handleSelect(params.id)}
          className='w-5 h-5 mt-1 rounded-lg float-right accent-red-500'></input>
      </p>
    </div>
  )
}

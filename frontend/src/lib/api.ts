import { FileInfoProps } from "@/types"
import axios from "axios"

const API_KEY = process.env.XD_API_KEY

if (!API_KEY) {
  throw new Error("XD_API_KEY is not defined")
}

const BASE_URL = process.env.BASE_URL

if (!BASE_URL) {
  throw new Error("BASE_URL is not defined")
}

const fetcher = axios.create({
  baseURL: BASE_URL,
  timeout: 3000,
  headers: {
    Authorization: `Bearer ${API_KEY}`,
  },
})

export const get_list = async (): Promise<FileInfoProps[]> => {
  const response = await fetcher.get("/list/")
  return response.data
}

export const upload_file = async (files: FileList) => {
  const fileList = Object.values(files)
  fileList.forEach(async (file) => {
    const formData = new FormData()
    formData.append("file", file)
    await fetcher.post("/upload/", formData)
    console.log("upload success")
  })
}

export const delete_file = async (ids: string[]) => {
  await fetcher.post("/delete/", { file_ids: ids })
  console.log("delete success")
  return true
}

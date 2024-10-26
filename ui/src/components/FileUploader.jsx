import { useState } from 'react'
import JSZip from 'jszip'
import { processFile } from '../utils/fileProcessing'

function FileUploader({ setSchema }) {
  const [isLoading, setIsLoading] = useState(false)

  const processFiles = async (files) => {
    const schema = {}

    for (const file of files) {
      const path = file.name.split('/')
      let current = schema

      for (let i = 0; i < path.length; i++) {
        if (i === path.length - 1) {
          current[path[i]] = await processFile(file)
        } else {
          current[path[i]] = current[path[i]] || {}
          current = current[path[i]]
        }
      }
    }

    return schema
  }

  const handleFileUpload = async (event) => {
    const files = event.target.files
    if (!files || files.length === 0) return

    setIsLoading(true)

    try {
      let schema = {}

      if (files[0].type === 'application/zip' || files[0].type === 'application/x-zip-compressed') {
        const zip = new JSZip()
        const contents = await zip.loadAsync(files[0])
        const zipFiles = Object.values(contents.files).filter(file => !file.dir)
        schema = await processFiles(zipFiles)
      } else {
        // Handle folder upload
        schema = await processFolder(files)
      }

      setSchema(schema)
    } catch (error) {
      console.error('Error generating schema:', error)
      alert('Failed to generate schema. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const processFolder = async (files) => {
    const schema = {}

    for (const file of files) {
      const path = file.webkitRelativePath.split('/')
      let current = schema

      for (let i = 0; i < path.length; i++) {
        if (i === path.length - 1) {
          current[path[i]] = await processFile(file)
        } else {
          current[path[i]] = current[path[i]] || {}
          current = current[path[i]]
        }
      }
    }

    return schema
  }

  return (
    <div>
      <input type="file" onChange={handleFileUpload} accept=".zip,.rar,.7zip" />
      <input type="file" onChange={handleFileUpload} webkitdirectory="" directory="" />
      {isLoading && <p>Generating schema...</p>}
    </div>
  )
}

export default FileUploader

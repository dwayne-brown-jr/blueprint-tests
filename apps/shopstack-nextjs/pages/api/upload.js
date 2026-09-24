import formidable from 'formidable'
import fs from 'fs'
export const config = { api: { bodyParser: false } }
// customers upload engraving artwork
export default async function handler(req, res) {
  const form = formidable({ uploadDir: './public/uploads', keepExtensions: true })
  form.parse(req, (err, fields, files) => res.json({ url: '/uploads/' + files.file[0].newFilename }))
}

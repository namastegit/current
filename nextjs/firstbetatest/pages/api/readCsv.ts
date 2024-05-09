// pages/api/csvData.ts
import fs from 'fs';
import csvParser from 'csv-parser';
import { NextApiRequest, NextApiResponse } from 'next';
import path from 'path'; // Import path module

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    // Resolve the absolute path to the CSV file
    const csvFilePath = path.resolve('./data.csv');

    const csvData = await new Promise<any[]>((resolve, reject) => {
      const parsedData: any[] = [];
      fs.createReadStream(csvFilePath)
        .pipe(csvParser())
        .on('data', (row) => {
          parsedData.push(row);
        })
        .on('end', () => {
          resolve(parsedData);
        })
        .on('error', (error) => {
          reject(error);
        });
    });

    res.status(200).json(csvData);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
}

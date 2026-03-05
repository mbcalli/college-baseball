import { useState, useEffect } from 'react'
import { getDataDates, DataDateInfo } from '../api'
import './DataStatusTerminal.css'

const DataStatusTerminal = () => {
  const [dataDates, setDataDates] = useState<DataDateInfo[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchDataDates = async () => {
      try {
        const response = await getDataDates()
        setDataDates(response.years)
        setLoading(false)
      } catch (err) {
        console.error('Error fetching data dates:', err)
        setLoading(false)
      }
    }

    fetchDataDates()
  }, [])

  if (loading || dataDates.length === 0) {
    return null
  }

  return (
    <div className="data-status-items">
    {dataDates.map((info) => (
        <div key={info.year} className="data-status-item">
        <span className="data-year">{info.year}:</span>
        <span className="data-date">{info.last_update}</span>
        </div>
    ))}
    </div>
  )
}

export default DataStatusTerminal

import * as React from "react"
import withClickable from "@/lib/withClickable"
import { Button } from "@/components/ui/button"

interface SkillButtonProps {
  uid: string
  name: string
  description: string
  stats: string
  onClick?: () => void
}

let SkillButtonBase = ({ uid, name, description, stats, onClick }: SkillButtonProps) => {
  return (
    <div className="space-y-2 p-4 border rounded-md">
      <Button uid={uid} onClick={onClick}>
        {name}
      </Button>
      <div className="text-sm">
        <h4 className="font-semibold">{name}</h4>
        <p>{description}</p>
        <div className="text-muted-foreground">
          {stats}
        </div>
      </div>
    </div>
  )
}

let SkillButton = withClickable(SkillButtonBase)

export { SkillButton }

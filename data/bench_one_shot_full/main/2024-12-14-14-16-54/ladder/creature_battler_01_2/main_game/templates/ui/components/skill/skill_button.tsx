import * as React from "react"
import { Button } from "@/components/ui/button"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps {
  uid: string
  name: string
  description: string
  stats: string
  onClick?: () => void
  disabled?: boolean
}

let SkillButton = ({
  uid,
  name,
  description,
  stats,
  onClick,
  disabled
}: SkillButtonProps) => {
  return (
    <div className="space-y-2">
      <Button 
        uid={`${uid}-button`}
        onClick={onClick}
        disabled={disabled}
      >
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

SkillButton = withClickable(SkillButton)

export { SkillButton }

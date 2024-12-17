import * as React from "react"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
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
    <HoverCard>
      <HoverCardTrigger asChild>
        <Button
          onClick={onClick}
          disabled={disabled}
        >
          {name}
        </Button>
      </HoverCardTrigger>
      <HoverCardContent>
        <div className="space-y-2">
          <h4 className="text-sm font-semibold">{name}</h4>
          <p className="text-sm">{description}</p>
          <div className="text-sm text-muted-foreground">
            {stats}
          </div>
        </div>
      </HoverCardContent>
    </HoverCard>
  )
}

SkillButton = withClickable(SkillButton)

export { SkillButton }

import * as React from "react"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
import { Button } from "@/components/ui/button"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps {
  uid: string
  name: string
  description: string
  stats: {
    damage?: number
    healing?: number
    cost?: number
  }
  onClick?: () => void
  disabled?: boolean
}

let SkillButtonBase = ({ uid, name, description, stats, onClick, disabled }: SkillButtonProps) => {
  return (
    <HoverCard uid={`${uid}-hover`}>
      <HoverCardTrigger uid={`${uid}-trigger`} asChild>
        <Button 
          onClick={onClick}
          disabled={disabled}
          className="w-[200px]"
          uid={`${uid}-button`}
        >
          {name}
        </Button>
      </HoverCardTrigger>
      <HoverCardContent uid={`${uid}-content`} className="w-[200px]">
        <div className="space-y-2">
          <h4 className="text-sm font-semibold">{name}</h4>
          <p className="text-sm text-muted-foreground">{description}</p>
          <div className="text-sm">
            {stats.damage && <div>Damage: {stats.damage}</div>}
            {stats.healing && <div>Healing: {stats.healing}</div>}
            {stats.cost && <div>Cost: {stats.cost}</div>}
          </div>
        </div>
      </HoverCardContent>
    </HoverCard>
  )
}

let SkillButton = withClickable(SkillButtonBase)

export { SkillButton }

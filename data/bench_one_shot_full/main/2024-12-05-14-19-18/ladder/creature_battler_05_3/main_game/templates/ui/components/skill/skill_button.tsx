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
    accuracy?: number
    type?: string
  }
}

let SkillButton = React.forwardRef<
  HTMLButtonElement,
  SkillButtonProps
>(({ uid, name, description, stats, ...props }, ref) => (
  <HoverCard uid={`${uid}-hover-card`}>
    <HoverCardTrigger uid={`${uid}-trigger`} asChild>
      <Button uid={`${uid}-button`} ref={ref} {...props}>
        {name}
      </Button>
    </HoverCardTrigger>
    <HoverCardContent uid={`${uid}-content`}>
      <div className="space-y-2">
        <h4 className="text-sm font-semibold">{name}</h4>
        <p className="text-sm">{description}</p>
        <div className="text-sm">
          {stats.damage && <div>Damage: {stats.damage}</div>}
          {stats.accuracy && <div>Accuracy: {stats.accuracy}%</div>}
          {stats.type && <div>Type: {stats.type}</div>}
        </div>
      </div>
    </HoverCardContent>
  </HoverCard>
))

SkillButton.displayName = "SkillButton"

SkillButton = withClickable(SkillButton)

export { SkillButton }

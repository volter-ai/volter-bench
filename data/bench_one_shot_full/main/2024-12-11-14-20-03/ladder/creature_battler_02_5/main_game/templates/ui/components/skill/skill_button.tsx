import * as React from "react"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
import { Button } from "@/components/ui/button"
import withClickable from "@/lib/withClickable"

let SkillButtonProps = {
  uid: string,
  name: string,
  description: string,
  stats: {
    damage?: number,
    accuracy?: number,
    cost?: number
  },
  onClick?: () => void,
  disabled?: boolean
}

let BaseSkillButton = ({
  uid,
  name,
  description,
  stats,
  onClick,
  disabled
}: typeof SkillButtonProps) => {
  return (
    <HoverCard uid={uid}>
      <HoverCardTrigger uid={`${uid}-trigger`} asChild>
        <Button
          uid={`${uid}-button`}
          onClick={onClick}
          disabled={disabled}
          className="w-full"
        >
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
            {stats.cost && <div>Cost: {stats.cost}</div>}
          </div>
        </div>
      </HoverCardContent>
    </HoverCard>
  )
}

let SkillButton = withClickable(BaseSkillButton)

export { SkillButton }

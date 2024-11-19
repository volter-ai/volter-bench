import * as React from "react"
import { Button } from "@/components/ui/button"
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps {
  uid: string
  name: string
  description: string
  damage?: number
  accuracy?: number
  children?: React.ReactNode
}

let SkillButton = ({ uid, name, description, damage, accuracy, children, ...props }: SkillButtonProps) => {
  return (
    <HoverCard uid={`${uid}-hover`}>
      <HoverCardTrigger uid={`${uid}-trigger`} asChild>
        <Button uid={`${uid}-button`} variant="default" {...props}>
          {name}
        </Button>
      </HoverCardTrigger>
      <HoverCardContent uid={`${uid}-content`}>
        <div className="space-y-2">
          <h4 className="text-sm font-semibold">{name}</h4>
          <p className="text-sm">{description}</p>
          {damage && <p className="text-sm">Damage: {damage}</p>}
          {accuracy && <p className="text-sm">Accuracy: {accuracy}%</p>}
        </div>
      </HoverCardContent>
    </HoverCard>
  )
}

SkillButton = withClickable(SkillButton)

export { SkillButton }

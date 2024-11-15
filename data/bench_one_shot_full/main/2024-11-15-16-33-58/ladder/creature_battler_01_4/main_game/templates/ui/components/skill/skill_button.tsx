import * as React from "react"
import withClickable from "@/lib/withClickable"
import { HoverCard as BaseHoverCard, HoverCardContent as BaseHoverCardContent, HoverCardTrigger as BaseHoverCardTrigger } from "@/components/ui/hover-card"
import { Button as BaseButton } from "@/components/ui/button"

interface SkillButtonProps {
  uid: string
  name: string
  description: string
  stats: string
  onClick?: () => void
  disabled?: boolean
}

let HoverCard = withClickable(BaseHoverCard)
let HoverCardTrigger = withClickable(BaseHoverCardTrigger)
let HoverCardContent = withClickable(BaseHoverCardContent)
let Button = withClickable(BaseButton)

let SkillButton = ({ uid, name, description, stats, onClick, disabled }: SkillButtonProps) => {
  return (
    <HoverCard uid={`${uid}-hover`}>
      <HoverCardTrigger uid={`${uid}-trigger`} asChild>
        <Button 
          onClick={onClick}
          disabled={disabled}
          variant="default"
          uid={`${uid}-button`}
        >
          {name}
        </Button>
      </HoverCardTrigger>
      <HoverCardContent uid={`${uid}-content`}>
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

export { SkillButton }

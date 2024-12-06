import * as React from "react"
import { HoverCard as BaseHoverCard, HoverCardContent as BaseHoverCardContent, HoverCardTrigger as BaseHoverCardTrigger } from "@/components/ui/hover-card"
import { Button as BaseButton } from "@/components/ui/button"
import withClickable from "@/lib/withClickable"

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

let SkillButton = ({
  uid,
  name,
  description,
  stats,
  onClick,
  disabled
}: SkillButtonProps) => {
  return (
    <HoverCard uid={uid}>
      <HoverCardTrigger uid={`${uid}-trigger`} asChild>
        <Button
          uid={`${uid}-button`}
          onClick={onClick}
          disabled={disabled}
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

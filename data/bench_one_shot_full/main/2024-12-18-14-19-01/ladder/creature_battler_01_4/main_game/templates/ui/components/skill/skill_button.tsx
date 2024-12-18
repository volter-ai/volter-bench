import * as React from "react"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
import { Button } from "@/components/ui/button"
import { HoverCardProps } from "@radix-ui/react-hover-card"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends HoverCardProps {
  uid: string
  name: string
  description: string
  stats: string
  onClick?: () => void
}

let SkillButtonComponent = ({ uid, name, description, stats, onClick, ...props }: SkillButtonProps) => {
  return (
    <HoverCard uid={uid} {...props}>
      <HoverCardTrigger uid={`${uid}-trigger`} asChild>
        <Button uid={`${uid}-button`} onClick={onClick}>{name}</Button>
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

let SkillButton = withClickable(SkillButtonComponent)

export { SkillButton }

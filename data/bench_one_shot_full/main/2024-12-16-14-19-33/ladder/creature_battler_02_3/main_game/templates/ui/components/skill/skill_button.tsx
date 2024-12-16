import * as React from "react"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/templates/ui/components/hover_card"
import { Button } from "@/templates/ui/components/button"

interface SkillButtonProps {
  uid: string
  name: string
  description: string
  stats: {
    damage?: number
    accuracy?: number
    [key: string]: any
  }
  onClick?: () => void
  disabled?: boolean
}

let SkillButton = ({
  uid,
  name,
  description,
  stats,
  onClick,
  disabled,
  ...props
}: SkillButtonProps) => {
  return (
    <HoverCard uid={uid}>
      <HoverCardTrigger uid={`${uid}-trigger`} asChild>
        <Button
          uid={`${uid}-button`}
          onClick={onClick}
          disabled={disabled}
          {...props}
        >
          {name}
        </Button>
      </HoverCardTrigger>
      <HoverCardContent uid={`${uid}-content`}>
        <div className="space-y-2">
          <h4 className="font-medium leading-none">{name}</h4>
          <p className="text-sm text-muted-foreground">{description}</p>
          <div className="text-sm">
            {Object.entries(stats).map(([key, value]) => (
              <div key={key}>
                {key}: {value}
              </div>
            ))}
          </div>
        </div>
      </HoverCardContent>
    </HoverCard>
  )
}

export { SkillButton }

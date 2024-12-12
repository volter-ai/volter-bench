import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface BaseCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

interface CreatureCardProps extends BaseCardProps {
  name: string
  hp: number
  maxHp: number
  imageUrl: string
}

let BaseCard = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <Card ref={ref} className={cn("", className)} uid={uid} {...props} />
  )
)

let BaseCardHeader = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardHeader ref={ref} className={cn("", className)} uid={uid} {...props} />
  )
)

let BaseCardTitle = React.forwardRef<HTMLParagraphElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardTitle ref={ref} className={cn("", className)} uid={uid} {...props} />
  )
)

let BaseCardContent = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardContent ref={ref} className={cn("", className)} uid={uid} {...props} />
  )
)

BaseCard.displayName = "BaseCard"
BaseCardHeader.displayName = "BaseCardHeader"
BaseCardTitle.displayName = "BaseCardTitle"
BaseCardContent.displayName = "BaseCardContent"

BaseCard = withClickable(BaseCard)
BaseCardHeader = withClickable(BaseCardHeader)
BaseCardTitle = withClickable(BaseCardTitle)
BaseCardContent = withClickable(BaseCardContent)

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <BaseCard ref={ref} className={cn("w-[300px]", className)} uid={uid} {...props}>
        <BaseCardHeader uid={`${uid}-header`}>
          <BaseCardTitle uid={`${uid}-title`}>{name}</BaseCardTitle>
          <div className="text-sm text-muted-foreground">
            HP: {hp}/{maxHp}
          </div>
        </BaseCardHeader>
        <BaseCardContent uid={`${uid}-content`}>
          <img
            src={imageUrl}
            alt={name}
            className="w-full h-[200px] object-contain"
          />
        </BaseCardContent>
      </BaseCard>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }

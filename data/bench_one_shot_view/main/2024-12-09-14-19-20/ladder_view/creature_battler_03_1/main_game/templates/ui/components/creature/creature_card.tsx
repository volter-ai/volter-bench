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

let CustomCard = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <Card ref={ref} className={className} {...props} />
  )
)

let CustomCardHeader = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardHeader ref={ref} className={className} {...props} />
  )
)

let CustomCardTitle = React.forwardRef<HTMLParagraphElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardTitle ref={ref} className={className} {...props} />
  )
)

let CustomCardContent = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardContent ref={ref} className={className} {...props} />
  )
)

CustomCard.displayName = "CustomCard"
CustomCardHeader.displayName = "CustomCardHeader"
CustomCardTitle.displayName = "CustomCardTitle"
CustomCardContent.displayName = "CustomCardContent"

CustomCard = withClickable(CustomCard)
CustomCardHeader = withClickable(CustomCardHeader)
CustomCardTitle = withClickable(CustomCardTitle)
CustomCardContent = withClickable(CustomCardContent)

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <CustomCard ref={ref} uid={uid} className={cn("w-[300px]", className)} {...props}>
        <CustomCardHeader uid={`${uid}-header`}>
          <CustomCardTitle uid={`${uid}-title`}>{name}</CustomCardTitle>
          <div className="text-sm text-muted-foreground">
            HP: {hp}/{maxHp}
          </div>
        </CustomCardHeader>
        <CustomCardContent uid={`${uid}-content`}>
          <img
            src={imageUrl}
            alt={name}
            className="w-full h-[200px] object-contain"
          />
        </CustomCardContent>
      </CustomCard>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }

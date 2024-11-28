import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle, CardProps, CardHeaderProps, CardContentProps, CardTitleProps } from "@/components/ui/card"
import { Progress, ProgressProps } from "@/components/ui/progress"
import withClickable from "@/lib/withClickable"

interface CreatureCardProps extends CardProps {
  uid: string
  name: string
  hp: number
  maxHp: number
  imageUrl: string
}

interface CreatureCardHeaderProps extends CardHeaderProps {
  uid: string
}

interface CreatureCardContentProps extends CardContentProps {
  uid: string
}

interface CreatureCardTitleProps extends CardTitleProps {
  uid: string
}

interface CreatureProgressProps extends ProgressProps {
  uid: string
}

let CreatureProgress = React.forwardRef<HTMLDivElement, CreatureProgressProps>(
  ({ uid, ...props }, ref) => <Progress ref={ref} {...props} />
)

let CreatureCardTitle = React.forwardRef<HTMLParagraphElement, CreatureCardTitleProps>(
  ({ uid, ...props }, ref) => <CardTitle ref={ref} {...props} />
)

let CreatureCardHeader = React.forwardRef<HTMLDivElement, CreatureCardHeaderProps>(
  ({ uid, ...props }, ref) => <CardHeader ref={ref} {...props} />
)

let CreatureCardContent = React.forwardRef<HTMLDivElement, CreatureCardContentProps>(
  ({ uid, ...props }, ref) => <CardContent ref={ref} {...props} />
)

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <Card ref={ref} className={cn("w-[300px]", className)} {...props}>
        <CreatureCardHeader uid={`${uid}-header`}>
          <CreatureCardTitle uid={`${uid}-title`}>{name}</CreatureCardTitle>
        </CreatureCardHeader>
        <CreatureCardContent uid={`${uid}-content`} className="grid gap-4">
          <img 
            src={imageUrl}
            alt={name}
            className="w-full h-48 object-contain"
          />
          <div className="flex items-center gap-2">
            <span className="text-sm">HP: {hp}/{maxHp}</span>
            <CreatureProgress uid={`${uid}-progress`} value={(hp / maxHp) * 100} />
          </div>
        </CreatureCardContent>
      </Card>
    )
  }
)

CreatureProgress.displayName = "CreatureProgress"
CreatureCardTitle.displayName = "CreatureCardTitle"
CreatureCardHeader.displayName = "CreatureCardHeader"
CreatureCardContent.displayName = "CreatureCardContent"
CreatureCard.displayName = "CreatureCard"

CreatureProgress = withClickable(CreatureProgress)
CreatureCardTitle = withClickable(CreatureCardTitle)
CreatureCardHeader = withClickable(CreatureCardHeader)
CreatureCardContent = withClickable(CreatureCardContent)
CreatureCard = withClickable(CreatureCard)

export { CreatureCard, CreatureCardHeader, CreatureCardContent, CreatureCardTitle, CreatureProgress }

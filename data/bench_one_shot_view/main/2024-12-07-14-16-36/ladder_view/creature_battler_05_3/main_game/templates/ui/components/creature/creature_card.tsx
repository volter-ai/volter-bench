import * as React from "react"
import { cn } from "@/lib/utils"
import { Card as BaseCard, CardContent as BaseCardContent, CardHeader as BaseCardHeader, CardTitle as BaseCardTitle } from "@/components/ui/card"
import { Progress as BaseProgress } from "@/components/ui/progress"
import withClickable from "@/lib/withClickable"

interface CardProps extends React.ComponentProps<typeof BaseCard> {
  uid: string
}

interface CardContentProps extends React.ComponentProps<typeof BaseCardContent> {
  uid: string
}

interface CardHeaderProps extends React.ComponentProps<typeof BaseCardHeader> {
  uid: string
}

interface CardTitleProps extends React.ComponentProps<typeof BaseCardTitle> {
  uid: string
}

interface ProgressProps extends React.ComponentProps<typeof BaseProgress> {
  uid: string
}

let Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ uid, ...props }, ref) => <BaseCard ref={ref} {...props} />
)

let CardContent = React.forwardRef<HTMLDivElement, CardContentProps>(
  ({ uid, ...props }, ref) => <BaseCardContent ref={ref} {...props} />
)

let CardHeader = React.forwardRef<HTMLDivElement, CardHeaderProps>(
  ({ uid, ...props }, ref) => <BaseCardHeader ref={ref} {...props} />
)

let CardTitle = React.forwardRef<HTMLParagraphElement, CardTitleProps>(
  ({ uid, ...props }, ref) => <BaseCardTitle ref={ref} {...props} />
)

let Progress = React.forwardRef<HTMLDivElement, ProgressProps>(
  ({ uid, ...props }, ref) => <BaseProgress ref={ref} {...props} />
)

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
  currentHp: number
  maxHp: number
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, imageUrl, currentHp, maxHp, ...props }, ref) => {
    return (
      <Card uid={`${uid}-card`} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
        </CardHeader>
        <CardContent uid={`${uid}-content`}>
          <div className="flex flex-col gap-4">
            <img 
              src={imageUrl}
              alt={name}
              className="w-full h-[200px] object-contain"
            />
            <Progress uid={`${uid}-progress`} value={(currentHp / maxHp) * 100} />
            <div className="text-sm text-center">
              {currentHp} / {maxHp} HP
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }
)

Card.displayName = "Card"
CardContent.displayName = "CardContent"
CardHeader.displayName = "CardHeader"
CardTitle.displayName = "CardTitle"
Progress.displayName = "Progress"
CreatureCard.displayName = "CreatureCard"

Card = withClickable(Card)
CardContent = withClickable(CardContent)
CardHeader = withClickable(CardHeader)
CardTitle = withClickable(CardTitle)
Progress = withClickable(Progress)
CreatureCard = withClickable(CreatureCard)

export { CreatureCard }

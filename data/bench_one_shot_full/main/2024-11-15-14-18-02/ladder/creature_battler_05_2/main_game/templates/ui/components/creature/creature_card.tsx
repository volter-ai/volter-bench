import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { 
  Card as BaseCard,
  CardContent as BaseCardContent, 
  CardHeader as BaseCardHeader,
  CardTitle as BaseCardTitle 
} from "@/components/ui/card"
import { Progress as BaseProgress } from "@/components/ui/progress"

let Progress = React.forwardRef<HTMLDivElement, React.ComponentProps<typeof BaseProgress> & { uid: string }>(
  ({ uid, ...props }, ref) => <BaseProgress {...props} ref={ref} />
)

let Card = React.forwardRef<HTMLDivElement, React.ComponentProps<typeof BaseCard> & { uid: string }>(
  ({ uid, ...props }, ref) => <BaseCard {...props} ref={ref} />
)

let CardContent = React.forwardRef<HTMLDivElement, React.ComponentProps<typeof BaseCardContent> & { uid: string }>(
  ({ uid, ...props }, ref) => <BaseCardContent {...props} ref={ref} />
)

let CardHeader = React.forwardRef<HTMLDivElement, React.ComponentProps<typeof BaseCardHeader> & { uid: string }>(
  ({ uid, ...props }, ref) => <BaseCardHeader {...props} ref={ref} />
)

let CardTitle = React.forwardRef<HTMLParagraphElement, React.ComponentProps<typeof BaseCardTitle> & { uid: string }>(
  ({ uid, ...props }, ref) => <BaseCardTitle {...props} ref={ref} />
)

Progress.displayName = "Progress"
Card.displayName = "Card"
CardContent.displayName = "CardContent"
CardHeader.displayName = "CardHeader"
CardTitle.displayName = "CardTitle"

Progress = withClickable(Progress)
Card = withClickable(Card)
CardContent = withClickable(CardContent)
CardHeader = withClickable(CardHeader)
CardTitle = withClickable(CardTitle)

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
      <Card uid={uid} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
        </CardHeader>
        <CardContent uid={`${uid}-content`}>
          <div className="flex flex-col gap-4">
            <img
              src={imageUrl}
              alt={name}
              className="h-[200px] w-full object-contain"
            />
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>HP</span>
                <span>{`${currentHp}/${maxHp}`}</span>
              </div>
              <Progress uid={`${uid}-progress`} value={(currentHp / maxHp) * 100} />
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
